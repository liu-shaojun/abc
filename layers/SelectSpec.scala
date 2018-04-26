/*
 * Copyright 2018 Analytics Zoo Authors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package com.intel.analytics.zoo.pipeline.api.keras.layers

import com.intel.analytics.bigdl.nn.{Select => BSelect}
import com.intel.analytics.zoo.pipeline.api.keras.layers.{Select => ZSelect}
import com.intel.analytics.bigdl.tensor.Tensor
import com.intel.analytics.bigdl.utils.Shape
import com.intel.analytics.zoo.pipeline.api.keras.ZooSpecHelper
import com.intel.analytics.zoo.pipeline.api.keras.serializer.ModuleSerializationTest

import scala.util.Random

class SelectSpec extends ZooSpecHelper {

  "Select Zoo 2D" should "be the same as BigDL" in {
    val blayer = BSelect[Float](2, 3)
    val zlayer = ZSelect[Float](1, 2, inputShape = Shape(5))
    zlayer.build(Shape(-1, 5))
    zlayer.getOutputShape().toSingle().toArray should be (Array(-1))
    val input = Tensor[Float](Array(4, 5)).rand()
    compareOutputAndGradInput(blayer, zlayer, input)
  }

  "Select Zoo 3D" should "be the same as BigDL" in {
    val blayer = BSelect[Float](2, -1)
    val zlayer = ZSelect[Float](1, -1, inputShape = Shape(3, 4))
    zlayer.build(Shape(-1, 3, 4))
    zlayer.getOutputShape().toSingle().toArray should be (Array(-1, 4))
    val input = Tensor[Float](Array(5, 3, 4)).rand()
    compareOutputAndGradInput(blayer, zlayer, input)
  }

  "Select Zoo 4D" should "be the same as BigDL" in {
    val blayer = BSelect[Float](3, 1)
    val zlayer = ZSelect[Float](2, 0, inputShape = Shape(3, 4, 5))
    zlayer.build(Shape(-1, 3, 4, 5))
    zlayer.getOutputShape().toSingle().toArray should be (Array(-1, 3, 5))
    val input = Tensor[Float](Array(2, 3, 4, 5)).rand()
    compareOutputAndGradInput(blayer, zlayer, input)
  }

  "Select Zoo with negative dim and index" should "be the same as BigDL" in {
    val blayer = BSelect[Float](-1, -1)
    val zlayer = ZSelect[Float](-1, -1, inputShape = Shape(3, 4, 5))
    zlayer.build(Shape(-1, 3, 4, 5))
    zlayer.getOutputShape().toSingle().toArray should be (Array(-1, 3, 4))
    val input = Tensor[Float](Array(2, 3, 4, 5)).rand()
    compareOutputAndGradInput(blayer, zlayer, input)
  }

  "Select the batch dimension" should "raise an exception" in {
    intercept[RuntimeException] {
      val zlayer = ZSelect[Float](0, 0, inputShape = Shape(2, 3, 4))
      zlayer.build(Shape(-1, 2, 3, 4))
    }
  }

  "Select dim out of range" should "raise an exception" in {
    intercept[RuntimeException] {
      val zlayer = ZSelect[Float](4, 0, inputShape = Shape(2, 3, 4))
      zlayer.build(Shape(-1, 2, 3, 4))
    }
  }

  "Select index out of range" should "raise an exception" in {
    intercept[RuntimeException] {
      val zlayer = ZSelect[Float](1, 3, inputShape = Shape(2, 3, 4))
      zlayer.build(Shape(-1, 2, 3, 4))
    }
  }

}

class SelectSerialTest extends ModuleSerializationTest {
  override def test(): Unit = {
    val layer = ZSelect[Float](-1, -1, inputShape = Shape(3, 4, 5))
    layer.build(Shape(2, 3, 4, 5))
    val input = Tensor[Float](2, 3, 4, 5).apply1(_ => Random.nextFloat())
    runSerializationTest(layer, input)
  }
}
